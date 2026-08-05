/*
==================================================
Dashboard API
==================================================
*/

class DashboardAPI {

    static async load() {

        const response = await fetch("/api/v1/dashboard");

        return await response.json();

    }

    static async refresh() {

        return await this.load();

    }

}