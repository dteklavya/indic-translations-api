import express from "express";
import { nmt, asr, tts, asr_nmt } from "../controllers/bhashini.controllers.mjs";

const router = express.Router()

router.get("/", (req, res) => {
    res.send("Welcome!")
})


router.post("/nmt", nmt);
router.post("/asr", asr);
router.post("/tts", tts);
router.post("/asr_nmt", asr_nmt);

export default router
