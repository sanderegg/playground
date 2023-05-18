const { Cluster } = require('puppeteer-cluster');
const fs = require('fs/promises');

async function acceptCookies(page) {
    const id = '[osparc-test-id=acceptCookiesBtn]';
    await page.waitForSelector(id, {
        timeout: 5000
    })
        .then(() => page.click(id))
        .catch(() => console.log("Accept Cookies button not found"));
}

async function logIn(page, user, pass) {
    // user might be already logged in
    const elementExists = await page.$('[osparc-test-id="userMenuMainBtn"]');
    if (elementExists !== null) {
        return;
    }

    // NOTE: since environ WEBSERVER_LOGIN_REGISTRATION_CONFIRMATION_REQUIRED=0, the
    // backend automatically creates session after registration is submitted
    console.log("Logging in:", user);
    await page.waitForSelector('[osparc-test-id="loginUserEmailFld"]', {
        visible: true,
        timeout: 10000
    });
    await page.type('[osparc-test-id="loginUserEmailFld"]', user);
    await page.waitForSelector('[osparc-test-id="loginPasswordFld"]');
    await page.type('[osparc-test-id="loginPasswordFld"]', pass);
    await Promise.all([page.waitForSelector('[osparc-test-id="loginSubmitBtn"]'), page.click('[osparc-test-id="loginSubmitBtn"]')]);
}

(async () => {
    // Create a cluster with 2 workers
    const cluster = await Cluster.launch({
        concurrency: Cluster.CONCURRENCY_BROWSER,
        maxConcurrency: 10,
        monitor: true,
        puppeteerOptions: { headless: true, defaultViewport: { width: 1240, height: 700 } }
    });
    // prepare screenshots folder
    const folderName = 'screenshots';
    await fs.rm(folderName, { recursive: true, force: true });
    await fs.mkdir(folderName, { recursive: true });

    // Event handler to be called in case of problems
    cluster.on('taskerror', (err, data) => {
        console.log(`Error crawling ${data}: ${err.message}`);
    });

    // Define a task (in this case: screenshot of page)
    await cluster.task(async ({ page, data, worker }) => {

        await page.goto(data.url, { waitUntil: 'networkidle0' });
        const basePath = folderName + "/" + worker.id + "_" + data.url.replace(/[^a-zA-Z]/g, '_');
        const screenshotExt = ".jpg"
        let path = basePath + "_" + "landing_page" + screenshotExt;
        await page.screenshot({ path, type: 'jpeg', quality: 50 });

        await acceptCookies(page)
        path = basePath + "_" + "accepted_cookies" + screenshotExt;
        await page.screenshot({ path, type: 'jpeg', quality: 50 });

        await logIn(page, data.user_prefix + (worker.id + 1) + data.user_suffix, data.password);
        await page.screenshot({ path: basePath + "_" + "logged_in" + screenshotExt, type: 'jpeg', quality: 50 });
    });

    // Add some pages to queue
    cluster.queue({ url: 'https://staging.osparc.io', user_prefix: "puppeteer_", user_suffix: "@itis.testing", password: "sadnap" });
    cluster.queue('https://staging.osparc.io');
    cluster.queue('https://staging.osparc.io');

    // Shutdown after everything is done
    await cluster.idle();
    await cluster.close();
})();