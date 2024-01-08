import express from 'express'
import cors from 'cors'
import config from 'dotenv'

import bhashini from 'bhashini-translation'
import nmt from './controllers/bhashini.controllers.js'

const app = express()
const port = 3000

const router = express.Router();

/* Global middlewares */
app.use(cors())
app.use(express.json())

config.config()
const userId = process.env.userID
const ulcaApiKey = process.env.ulcaApiKey
const inferenceApiKey = process.env.InferenceApiKey

bhashini.auth(userId, ulcaApiKey, inferenceApiKey)

app.get("/", (req, res) => {
    res.send("Welcome!")
})

app.post("/nmt", async (req, res) => {
    return await nmt(req, res)
})


/* Server startup */
if (process.env.NODE_ENV !== 'test') {
    app.listen(port, () => console.log(`⚡️[server]: Server is running at https://localhost:${port}`))
}

export default app
