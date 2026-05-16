@app.post("/contact")
async def contact(form: ContactForm):

    await send_email(
        form.name,
        form.email,
        form.message
    )

    return {
        "message": "Message sent successfully!"
    }
