/*
==================================================
Profile API
==================================================
*/

class ProfileAPI {

    static async getProfile() {

        const response = await fetch("/api/v1/profile");

        return await response.json();

    }

    static async update(data) {

        const response = await fetch(

            "/api/v1/profile/update",

            {

                method: "POST",

                headers: {

                    "Content-Type":

                        "application/json"

                },

                body: JSON.stringify(data)

            }

        );

        return await response.json();

    }

}