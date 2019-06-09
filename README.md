# Lambda Function For CloudFront IP White Listing
This Lambda Code WhiteListed IP address given by AWS AmazonIpSpaceChanged SNS Service.

# Steps to create Lambda function in AWS

1. Create functions [lambda_function.py](https://github.com/yash-sonani/LambdaForCloudFrontIPWhiteListing/blob/master/lambda_function.py) , [Support.py](https://github.com/yash-sonani/LambdaForCloudFrontIPWhiteListing/blob/master/Support.py) and [SG_Operation.py](https://github.com/yash-sonani/LambdaForCloudFrontIPWhiteListing/blob/master/SG_Operation.py)

2. Create SNS trigger in Lambda with [arn:aws:sns:us-east-1:806199016981:AmazonIpSpaceChanged](https://docs.aws.amazon.com/general/latest/gr/aws-ip-ranges.html)
