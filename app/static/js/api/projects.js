/*
==================================================
Projects API
==================================================
*/

class ProjectAPI {

    static async all() {

        const response = await fetch(

            "/api/v1/projects"

        );

        return await response.json();

    }

}