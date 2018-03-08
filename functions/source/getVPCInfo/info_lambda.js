var aws = require('aws-sdk');

exports.handler = (e, c) => {
 console.log('REQUEST RECEIVED:\\n' + JSON.stringify(e));

 // For Delete requests, immediately send a SUCCESS response.
 if (e.RequestType == 'Delete') {
    sendResponse(e, c, 'SUCCESS');
    return;
  }

  var ec2 = new aws.EC2({ region: e.ResourceProperties.Region });
  var vpc = e.ResourceProperties.VpcId;
  var func = e.ResourceProperties.Func;

  var status = 'FAILED';
  var responseData = {};
  if (func === 'DescribeVpc') {
    // Get VPCs with the specified id
    ec2.describeVpcs({ VpcIds: [vpc] }, (err, data) => {
      console.log('vpcs:\\n' + JSON.stringify(data));
      err = err || (data.Vpcs.length !== 1 ? 'DescribeVpcs returned ' + data.Vpcs.length + ' results.' : undefined);
      if (err) {
        responseData.Error = 'DescribeVpcs call failed';
        console.log(responseData.Error + ':\\n', err);
      } else {
        status = 'SUCCESS';
        responseData = data.Vpcs[0];
      }
      sendResponse(e, c, status, responseData);
    });
  } else {
    sendResponse(e, c, status, {Error: 'Unknown Function ' + func});
  }
};

// Send response to the pre-signed S3 URL
function sendResponse(e, c, status, responseData) {
  var responseBody = JSON.stringify({
    Status: status,
    Reason: 'See the details in CloudWatch Log Stream: ' + c.logStreamName,
    PhysicalResourceId: c.logStreamName,
    StackId: e.StackId,
    RequestId: e.RequestId,
    LogicalResourceId: e.LogicalResourceId,
    Data: responseData
  });

  console.log('RESPONSE BODY:\\n', responseBody);

  var https = require('https');
  var url = require('url');

  var parsedUrl = url.parse(e.ResponseURL);
  var options = {
    hostname: parsedUrl.hostname,
    port: 443,
    path: parsedUrl.path,
    method: 'PUT',
    headers: {
      'content-type': '',
      'content-length': responseBody.length
    }
  };

  console.log('SENDING RESPONSE...\\n');

var request = https.request(options, (response) => {
    console.log('STATUS: ' + response.statusCode);
    console.log('HEADERS: ' + JSON.stringify(response.headers));
    c.done(); // Tell AWS Lambda function execution is done
  });

  request.on('error', (err) => {
    console.log('sendResponse Error:' + err);
    c.done(); // Tell AWS Lambda function execution is done
  });

  // write data to request body
  request.write(responseBody);
  request.end();
}