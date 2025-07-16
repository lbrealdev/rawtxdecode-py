# Alias

alias lambda := invoke-lambda

# Variables

cwd := invocation_directory()
raw_tx_hex := '0x02f8b2018207a984010bef3384780f481a8301482094dac17f958d2ee523a2206206994597c13d831ec780b844a9059cbb000000000000000000000000a29e963992597b21bcdcaa969d571984869c4ff50000000000000000000000000000000000000000000000000000008e06d55400c080a063ec94403b94ef380a4c4c31b3df991ca456d84943f53e6d207d57d697a8ee98a01631a9ad2884defacfa06eca1d8cfc04c26b119f206a72006e8b0f1802ceab9f'

# Default recipes

@lint:
    ruff check .

@fmt:
    ruff format .

@run:
    uv run decode {{ raw_tx_hex }}

# Lambda recipes

[working-directory: 'app']
@invoke-lambda:
    uv run invoke_lambda.py

@lambda-pkg:
    echo "Create zip package"

    echo "Generating requirements.txt..."
    uv export --frozen --no-dev --no-editable -o requirements.txt

    echo "Creating packages directory..."
    uv pip install --no-installer-metadata --no-compile-bytecode --python-platform x86_64-manylinux2014 -p 3.12 --target packages -r requirements.txt

    echo "Creating zip file..."
    just zip-app

[working-directory: 'packages']
@zip-pkg:
    zip -qr {{ cwd }}/lambda_bundle.zip .

[working-directory: 'app']
@zip-app: (zip-pkg)
    zip -qr {{ cwd }}/lambda_bundle.zip main.py

@clean:
    rm -rf {{ cwd }}/lambda_bundle.zip {{ cwd }}/packages
