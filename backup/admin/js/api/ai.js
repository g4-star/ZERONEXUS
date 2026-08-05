/*
==================================================
ZeroNexus AI API
==================================================
*/

class AIAPI {

    static async prompts() {

        const response = await fetch(

            "/api/v1/ai/prompts"

        );

        return await response.json();

    }

    static async ask(prompt) {

        const response = await fetch(

            "/api/v1/ai/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":

                        "application/json"

                },

                body: JSON.stringify({

                    prompt: prompt

                })

            }

        );

        return await response.json();

    }

}/*
==================================================
ZeroNexus AI API
==================================================
*/

class AIAPI {

    static async prompts() {

        const response = await fetch(

            "/api/v1/ai/prompts"

        );

        return await response.json();

    }

    static async ask(prompt) {

        const response = await fetch(

            "/api/v1/ai/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":

                        "application/json"

                },

                body: JSON.stringify({

                    prompt: prompt

                })

            }

        );

        return await response.json();

    }

}/*
==================================================
ZeroNexus AI API
==================================================
*/

class AIAPI {

    static async prompts() {

        const response = await fetch(

            "/api/v1/ai/prompts"

        );

        return await response.json();

    }

    static async ask(prompt) {

        const response = await fetch(

            "/api/v1/ai/chat",

            {

                method: "POST",

                headers: {

                    "Content-Type":

                        "application/json"

                },

                body: JSON.stringify({

                    prompt: prompt

                })

            }

        );

        return await response.json();

    }

}