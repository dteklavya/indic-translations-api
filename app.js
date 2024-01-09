import express from 'express'
import cors from 'cors'
import config from 'dotenv'
import swaggerUI from 'swagger-ui-express'
import YAML from 'yamljs'

import bhashini from 'bhashini-translation'
import router from './routes/bhashini.routes.mjs'

const app = express()
const port = 3002

// swagger definition
const swaggerSpec = YAML.load('./swagger.yml') 

/* Global middlewares */
app.use(cors())
app.use(express.json())

config.config()
const userId = process.env.userID
const ulcaApiKey = process.env.ulcaApiKey
const inferenceApiKey = process.env.InferenceApiKey

bhashini.auth(userId, ulcaApiKey, inferenceApiKey)

app.use(
    '/api-docs',
    swaggerUI.serve,
    swaggerUI.setup(swaggerSpec)
)

app.use("/", router)


/* Server startup */
if (process.env.NODE_ENV !== 'test') {
    app.listen(port, () => console.log(`⚡️[server]: Server is running at https://localhost:${port}`))
}

export default app
