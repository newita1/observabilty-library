
//                                          o8o      .               
//                                          `"'    .o8             
//  ooo. .oo.    .ooooo.  oooo oooo    ooo oooo  .o888oo  .oooo.    
// `888P"Y88b  d88' `88b  `88. `88.  .8'  `888    888   `P  )88b    
//  888   888  888ooo888   `88..]88..8'    888    888    .oP"888    
//  888   888  888    .o    `888'`888'     888    888 . d8(  888   
// o888o o888o `Y8bod8P'     `8'  `8'     o888o   "888" `Y888""8o 

const { test, expect } = require('@playwright/test');

test('Acceder a checkmk', async ({ page }) => {
        await test.step('01. Load Webpage', async () => {
          await page.goto('https://service-now.com/',{waitUntil: 'load', timeout: 20000});	
        });
        
        await test.step('02. Login', async () => {
          await page.locator('input[id="user_name"]').fill("usuario");
          await page.locator('input[id="user_password"]').fill("contrasñea");
          await page.locator('button[name="not_important"]').click();  
        });     

        await test.step('03. Load HomePage', async () => {
          await page.locator('input[name="sncwsgs-typeahead-input"]').isEnabled();
          await page.getByPlaceholder('Search').click();
          await page.getByPlaceholder('Search Global').fill('BUSQUEDA');
          await page.getByRole('option', { name: 'TITLE | Service:' }).locator('span').isVisible({timeout : 30000});
      });

        await test.step('04. Load Host', async () => {
          await page.keyboard.press('Enter');
          await page.frameLocator('iframe[name="gsft_main"]').getByRole('textbox', { name: 'Read only - cannot be modifiedResuelto por' }).click({timeout : 30000});
        });
});

