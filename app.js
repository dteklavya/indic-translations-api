import express from 'express'
import cors from 'cors'
import config from 'dotenv'
import swaggerUI from 'swagger-ui-express'
import swaggerJSdoc from 'swagger-jsdoc'

import bhashini from 'bhashini-translation'
import nmt from './controllers/bhashini.controllers.mjs'
import router from './routes/bhashini.routes.mjs'

const app = express()
const port = 3002

// swagger definition
const swaggerSpec = {
    definition: {
        openapi: '3.0.0',
        info: {
            title: 'Bhashini API',
            version: '1.0.0',
        },
        servers: [
            {
                url: `http://localhost:${port}`,
            }
        ]
    },
    apis: ['./routes/*.mjs'],
}

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
    swaggerUI.setup(swaggerJSdoc(swaggerSpec))
)

app.use("/", router)


/* Server startup */
if (process.env.NODE_ENV !== 'test') {
    app.listen(port, () => console.log(`⚡️[server]: Server is running at https://localhost:${port}`))
}

export default app
