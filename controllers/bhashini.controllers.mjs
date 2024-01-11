import bhashini from "bhashini-translation"
import { tts_payload } from "bhashini-translation/config/payload.js"
import BaseApi from "bhashini-translation/src/utils/baseApi.js"
import fs from 'fs'

export const nmt = async (req, res) => {
    const sourceLanguage = req.body.sourceLanguage
    const targetLanguage = req.body.targetLanguage
    const text = req.body.text
    // console.log(sourceLanguage, targetLanguage, text)
    try {
        const result = await bhashini.nmt(sourceLanguage, targetLanguage, text)
        res.status(200).json(result)
    } catch (err) {
        res.status(500).send(err)
    }
}


export const asr = async (req, res) => {
    const sourceLanguage = req.body.sourceLanguage
    const base64String = req.body.audio
    try {
        const result = await bhashini.asr(sourceLanguage, base64String)

        res.status(200).json(result)
    } catch (err) {
        res.status(500).send(err)
    }
}

export const tts = async (req, res) => {
    const sourceLanguage = req.body.sourceLanguage
    const text = req.body.text
    const gender = req.body.gender

    const bhashiniApi = new BaseApi;
    const payload = await tts_payload(sourceLanguage, text, gender)
    try {
        const response = await bhashiniApi.post(payload)
        const result = await bhashini.tts(sourceLanguage, text, gender)
        let base64Sound = response.data.pipelineResponse[0].audio[0].audioContent;

        const buffer = Buffer.from(base64Sound, 'base64')
        const filename = `/tmp/audio_${Date.now()}.wav`;

        fs.writeFileSync(filename, buffer);

        // Send the file as the response
        res.status(200).sendFile(filename);
    } catch (err) {
        res.status(500).send(err)
    }
}

export default nmt 
