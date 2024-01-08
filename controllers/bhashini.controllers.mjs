import bhashini from "bhashini-translation"

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

export default nmt
