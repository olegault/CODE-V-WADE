//built using GW USEC script
//must edit for doc db


const mysql = require('mysql2');
const puppeteer = require('puppeteer');
const Xvfb = require('xvfb');
const fs = require('fs');
const winston = require('winston');
const url = require('url');
const path = require('path');
const { triggerAsyncId } = require('async_hooks');
require('dotenv').config();
require('events').EventEmitter.defaultMaxListeners = Infinity; 

const logger = winston.createLogger({
    level: process.env.logLevel,
    format: winston.format.json(),
    transports: [
        //
        // - Write all logs with level `error` and below to `error.log`
        // - Write all logs with level `info` and below to `combined.log`
        //
        new winston.transports.File({ filename: './log/error.log', level: 'error' }),
        new winston.transports.File({filename:'./log/debug.log', level:'debug'}),
        new winston.transports.File({ filename: './log/combined.log' }),
    ],
});

var existing_policies;

async function fetchPolicy (app_table_values) {
    let xvfb = new Xvfb({
        silent: triggerAsyncId,
        xvfb_args: ["-screen", "0", "1280x720x24", "-ac"]
    });
    xvfb.start((err) => {
        if (err) {
            console.error(error);
        }
    });
    let browser = await puppeteer.launch({
        headless: false,
        defaultViewport: null,
        ignoreHTTPSErrors: true,
        args: ['--no-sandbox', '--start-fullscreen', '--display='+xvfb._display]
    });
    for (let i = 0; i < app_table_values.length; i++) {

        let privacy_policy_url;
        try {
            privacy_policy_url = new URL(app_table_values[i].privacy_policy_url);
        } catch (error) {
            logger.error(`
                    Invalid URL.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
            continue;
        }

        if (existing_policies.includes(app_table_values[i].privacy_policy_url) || existing_policies.includes(privacy_policy_url)) {
            continue;
        }

        if (await checkIfExists(app_table_values[i].privacy_policy_url)) {
            continue;
        }

        let context;
        try {
            // Create a new incognito browser context
            context = await browser.createIncognitoBrowserContext();
            logger.debug(
                `
                Opened Incognito Context.
                Policy URL: ${app_table_values[i].privacy_policy_url}
                `);
        } catch (error) {
            logger.error(`
                    Failed to create a new Incognito Context.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
            continue;
        }
        let page;
        try {
            page = await context.newPage();
            logger.debug(
                `
                Opened New Page.
                Policy URL: ${app_table_values[i].privacy_policy_url}
                `);
        } catch(error) {
            logger.error(`
                    Failed to create a new page.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
            continue;
        }
        try {
            await page.goto(`${privacy_policy_url}`,{waitUntil: 'domcontentloaded'});
            logger.debug(
                `
                Loaded Page URL.
                Policy URL: ${app_table_values[i].privacy_policy_url}
                `);
        } catch (error) {
            logger.error(`
                    Error while connecting to URL.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
            // await page.close();
            await context.close();
            continue;
        }
        let pageContent = '';
        try {
            pageContent = await Promise.race([
                page.waitForNavigation(), // The promise resolves after navigation has finished
                page.content(), 
              ]);
            logger.debug(
                `
                Fetched Page Content.
                Policy URL: ${app_table_values[i].privacy_policy_url}
                `);
        } catch (error) {
            logger.error(`
                    Error fetching page content.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
            await page.close();
            await context.close();
            continue;
        }
        try {
            pageContent = encodeURIComponent(pageContent);
            logger.debug(
                `
                Page Content Loaded.
                Policy URL: ${app_table_values[i].privacy_policy_url}
                `);
        } catch (error) {
            logger.error(`
                    Error Encoding Received HTML Page Content.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
            await page.close();
            await context.close();
            continue;
        }
        try {
            await page.close();
            await context.close();
            logger.debug(
                `
                New Page and Context Closed.
                Policy URL: ${app_table_values[i].privacy_policy_url}
                `);
        } catch (error) {
            logger.error(`
                    Error Closing Page or Context.
                    Policy URL: ${app_table_values[i].privacy_policy_url}
                    Error Message: ${error}`
                );
        }
        await addPolicyToDb(app_table_values[i].privacy_policy_url, pageContent);
    }

}

async function checkIfExists(privacy_policy_url) {

    let connection;
    try {
        connection = mysql.createConnection({
        user: process.env.dbUser,
        password: process.env.dbPass,
        database: process.env.dbName
        });
        logger.debug(
            `
            Opened a connection to database.
            Privacy Policy URL: ${privacy_policy_url}
            `);
    } catch (error) {
        logger.error(`
            Error while opening a connection to the database.
            Privacy Policy URL: ${privacy_policy_url}
            Error Message: ${error}`
        );
    }

    existing_app = `
        SELECT id from run_43_raw_policy WHERE policy_url = "${privacy_policy_url}" OR policy_url = "${new URL(privacy_policy_url)}"
        `;
    
    try {
        result = await connection.promise().query(existing_app);
        logger.debug(
            `
            Queried database to check if policy already exists.
            Privacy Policy URL: ${privacy_policy_url}
            `);
    } catch (error) {
        logger.error(`
            Error while checking if policy exists in the database.
            Privacy Policy URL: ${privacy_policy_url}
            Error Message: ${error}`
        );
        return false;
    }

    try {
        connection.end();
        logger.debug(
            `
            Closed Database Connection.
            Privacy Policy URL: ${privacy_policy_url}
            `);
    } catch (error) {
        logger.error(`
            Error while closing database connection.
            Privacy Policy URL: ${privacy_policy_url}
            Error Message: ${error}`
        );
    }

    if (!(result[0].length > 0)) {
        logger.debug(
            `
            Policy does not exist in the database.
            Privacy Policy URL: ${privacy_policy_url}
            `);
        return false;
    } 

    
    return true;
    
}

async function addPolicyToDb(privacy_policy_url, raw_html) {

    let connection 
    try {
        connection = mysql.createConnection({
            //host: "localhost",
            user: process.env.dbUser,
            password: process.env.dbPass,
            database: process.env.dbName
          });
        logger.debug(
            `
            Opened a connection to database.
            Privacy Policy URL: ${privacy_policy_url}
            `);
    } catch (error) {
        logger.error(`
                Error while inserting into database.
                Privacy Policy URL: ${privacy_policy_url}
                Error Message: ${error}`
            );
    }

    policy_insert = `
        INSERT INTO run_43_raw_policy
        (
            policy_url
            , raw_html
        ) 
        VALUES ("${privacy_policy_url}", "${raw_html}")`;
    //.replace(/[\n\s]/g, '')
    
    try {
        result = await connection.promise().query(policy_insert);
        logger.debug(
            `
            Added 1 policy to the database.
            Privacy Policy URL: ${privacy_policy_url}
            `);
    } catch (error) {
        logger.error(`
            Error while inserting policy into database.
            Privacy Policy URL: ${privacy_policy_url}
            Error Message: ${error}`
        );
    }
    
    try {
        connection.end();
        logger.debug(
            `
            Closed Database Connection.
            Privacy Policy URL: ${privacy_policy_url}
            `);
    } catch (error) {
        logger.error(`
            Error while closing database connection.
            Privacy Policy URL: ${privacy_policy_url}
            Error Message: ${error}`
        );
    }

    return;
}

async function getPolicyUrls() {

    let results;
    let query = "SELECT DISTINCT(privacy_policy_url) from run_43 WHERE privacy_policy_url NOT IN (SELECT DISTINCT(policy_url) FROM run_43_raw_policy)"

    let connection = mysql.createConnection({
        //host: "localhost",
        user: process.env.dbUser,
        password: process.env.dbPass,
        database: process.env.dbName
      });
    
    connection.connect(function(err) {
        if (err) {
            logger.error(`
                Error while connecting to the database.
                Error Message: 
                ${err}`
            );
        }
        logger.debug(
            `
            Successfully connected to the database. Querying for policy URLs.
            `
        );
    });

    results = await connection.promise().query(query);

    connection.end();

    return results[0];
    
}

function convertToRowFormat(arr) {
    policy_urls_formatted = [];
    arr.forEach(policy_url => {
        policy_urls_formatted.push({
            "privacy_policy_url": policy_url
        })
    })
    return policy_urls_formatted;
}

async function readListFromFile(filename = 'policies.txt') {
    let contents = await fs.promises.readFile(filename, 'utf-8');

    let arr = contents.split(/\r?\n/);

    // console.log(arr); // 👉️ ['One', 'Two', 'Three', 'Four']

    return arr;
}

(async () => {
    existing_policies = await readListFromFile();
    // let app_table_values = await getPolicyUrls();
    // app_table_values = Object.values(app_table_values);
    let app_table_values = await readListFromFile('/home/mali92/2021-privacy-labels/policy_urls_na.txt');
    app_table_values = convertToRowFormat(app_table_values);
    let num_apps = app_table_values.length;
    Promise.all([
        fetchPolicy(app_table_values.slice(0, num_apps/10)),
        fetchPolicy(app_table_values.slice(num_apps/10, num_apps/10 * 2)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 2, num_apps/10 * 3)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 3, num_apps/10 * 4)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 4, num_apps/10 * 5)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 5, num_apps/10 * 6)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 6, num_apps/10 * 7)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 7, num_apps/10 * 8)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 8, num_apps/10 * 9)),
        fetchPolicy(app_table_values.slice(num_apps/10 * 9, num_apps)),
    ]);
})();
