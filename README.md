# rawtxdecode python

## Usage

> [!IMPORTANT]
> This CLI currently **supports only type 2 (EIP-1559) Ethereum transactions**.  
> Legacy transactions (type 0) and type 1 (EIP-2930) are not supported yet.

Export `ETHERSCAN_API_KEY`:
```shell
export ETHERSCAN_API_KEY="<api-key>"
```

Run the `decode` script by passing the raw transaction hex as an argument:
```shell
uv run decode <raw-transaction-hex>
```

Example:
```shell
uv run decode 0x02f8b2018207a984010bef3384780f481a8301482094dac17f958d2ee523a2206206994597c13d831ec780b844a9059cbb000000000000000000000000a29e963992597b21bcdcaa969d571984869c4ff50000000000000000000000000000000000000000000000000000008e06d55400c080a063ec94403b94ef380a4c4c31b3df991ca456d84943f53e6d207d57d697a8ee98a01631a9ad2884defacfa06eca1d8cfc04c26b119f206a72006e8b0f1802ceab9f
```

## Example Output (JSON)

```json
{
  "chainId": 1,
  "type": "EIP-1559",
  "valid": true,
  "hash": "0x5841ee016fb03c5b8f7753342564e52b344771d94b6c17cbaa89a5fafd448453",
  "nonce": 1961,
  "gasLimit": 84000,
  "maxFeePerGas": 2014267418,
  "maxPriorityFeePerGas": 17559347,
  "from": "0x3cb27abe5d9ef37f9866626c70624185a0e70142",
  "to": "0xdac17f958d2ee523a2206206994597c13d831ec7",
  "publicKey": "0x04ae779965c64b126f775d7fdb82723bd6914579ac2068639eaf3d08573ee36e5799d33b5e9c6a493ff24bae25c1a5d4566a764ee00928a5528ab2f1ef3aff9e31",
  "v": "00",
  "r": "63ec94403b94ef380a4c4c31b3df991ca456d84943f53e6d207d57d697a8ee98",
  "s": "1631a9ad2884defacfa06eca1d8cfc04c26b119f206a72006e8b0f1802ceab9f",
  "value": "0",
  "input": "0xa9059cbb000000000000000000000000a29e963992597b21bcdcaa969d571984869c4ff50000000000000000000000000000000000000000000000000000008e06d55400",
  "functionHash": "0xa9059cbb",
  "functionName": "transfer",
  "decodedInputs": {
    "_to": "0xa29E963992597B21bcDCaa969d571984869C4FF5",
    "_value": 610000000000
  }
}
```

## Development

```shell
uv add eth-account eth-utils hexbytes py-evm rlp
```
