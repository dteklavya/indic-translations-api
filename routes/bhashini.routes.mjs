import express from "express";
import nmt from "../controllers/bhashini.controllers.mjs";

const router = express.Router()

router.get("/", (req, res) => {
    res.send("Welcome!")
})
router.post("/nmt", nmt);

export default router
