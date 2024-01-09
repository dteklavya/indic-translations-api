import express from "express";
import { nmt, asr, tts } from "../controllers/bhashini.controllers.mjs";

const router = express.Router()

router.get("/", (req, res) => {
    res.send("Welcome!")
})


/**
 * @swagger
 * components:
 *  schemas:
 *     NMT:
 *      type: object
 *      properties:
 *          sourceLanguage:
 *              type: string
 *              description: Source Language
 *          targetLanguage:
 *              type: string
 *              description: Target Language
 *          text:
 *              type: string
 *              description: Text to translate
 */

/**
 * @swagger
 * /nmt:
 *  post:
 *     summary: Get translation
 *     description: Get translation from source to target language
 *     requestBody:
 *         description: A JSON object containing source and target languages and the text to translate
 *         content:
 *            application/json:
 *                schema:
 *                   $ref: '#/components/schemas/NMT'
 *     responses:
 *       200:
 *         description: Success
 *       500:
 *         description: Internal Server Error
 */
router.post("/nmt", nmt);
router.post("/asr", asr);
router.post("/tts", tts);

export default router
