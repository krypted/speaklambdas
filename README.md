

## Trigger Lambda function thru Alexa 
Designed to allow developers to create three or more functions, using some simple endpoints I already had in Postman for Walmart, Swiggy, Amazon & a parent function which will communicate with Alexa and will call/invoke the approperiate nested lambda functions

## Alexa skill model building
Use the models/en-US.json file for model building
  
## Invoke another lambda function
- Create policy and provide necessary access for those lambda function. FOr example,
```    {
        "Effect": "Allow",
        "Action": [            
            "lambda:*"
        ],
        "Resource": [            
            "arn:aws:lambda:us-east-1:xxxxxx:function:walmart",
            "arn:aws:lambda:us-east-1:xxxxxx:function:swiggy",
            "arn:aws:lambda:us-east-1:xxxxxx:function:amazon"

        ]
    }
```

- Attach this policy with the parent function in order to invoke the child functions


## Lambda package for deployment
- Install the required packages in the same directory by execute the below command
  `pip install -r requirements.txt --target=./`
- compress/zip the entire folder from inside the directory
- Upload the zip file to the aws lambda function
- Keep the HandlerInfo as lambda_function.handler


### Interations with Alexa,

User - Alexa, invoke the lambda skill
Alexa - Welcome message

User - can you please start the function walmart
Alexa - Speakout the child function's resp body message
