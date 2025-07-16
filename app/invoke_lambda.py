from main import lambda_handler
import json


RAW_TX_HEX = "0x02f8b2018207a984010bef3384780f481a8301482094dac17f958d2ee523a2206206994597c13d831ec780b844a9059cbb000000000000000000000000a29e963992597b21bcdcaa969d571984869c4ff50000000000000000000000000000000000000000000000000000008e06d55400c080a063ec94403b94ef380a4c4c31b3df991ca456d84943f53e6d207d57d697a8ee98a01631a9ad2884defacfa06eca1d8cfc04c26b119f206a72006e8b0f1802ceab9f"


if __name__ == "__main__":
    event = {"hex": RAW_TX_HEX}
    context = {}
    result = lambda_handler(event, context)
    
    # Default output (dict)
    # print(result)

    # Pretty output (json)
    print(json.dumps(result, indent=2))