
# LB Tasks API

Este proyecto implementa una API para gestionar tareas utilizando AWS Lambda, DynamoDB y API Gateway. La infraestructura está definida y desplegada con AWS CDK.

## Pre-requisitos

1. **AWS CLI**: Asegúrate de tener la CLI de AWS configurada:
   ```bash
   aws configure
   ```

2. **Node.js**: CDK requiere Node.js 20 o superior. Instálalo desde [nodejs.org](https://nodejs.org/).

3. **AWS CDK**: Instala CDK globalmente:
   ```bash
   npm install -g aws-cdk
   ```

4. **Python 3.9**: Asegúrate de tener Python 3.9 instalado.

---

## Despliegue local

1. **Instala las dependencias**:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Despliega el stack**:
   ```bash
   cdk deploy
   ```

---