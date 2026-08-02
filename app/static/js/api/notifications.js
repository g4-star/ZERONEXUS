/*
==================================================
Notifications API
==================================================
*/

class NotificationAPI {

    static async unread() {

        const response = await fetch(

            "/api/v1/notifications"

        );

        return await response.json();

    }

}