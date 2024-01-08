import express from "express";
import nmt from "../controllers/bhashini.controllers.mjs";

const router = express.Router()

router.post("/nmt", nmt);

export default router
