import { expect, type Locator, type Page } from '@playwright/test';

export class UniPage {
    readonly page: Page;
    readonly searchHeader: Locator;
    readonly searchStaff: Locator;
    readonly searchName: Locator;
    readonly searchButton: Locator;
    readonly linkName: Locator;
    readonly searchRoom: Locator;

    constructor(page: Page) {
        this.page = page 
        this.searchHeader = page.getByLabel('Nagłówek').getByRole('link', { name: 'Pracownicy' })
        this.searchStaff = page
            .locator('#views-bootstrap-prezentacja-w-kategorii-terminy-blok-poddzialy')
            .getByRole('link', { name: 'Skład osobowy' })
        this.searchName = page.getByRole('textbox', { name: 'Imię lub nazwisko' })
        this.searchButton = page.locator('#edit-submit-pracownik-szukaj')
        this.linkName = page.getByRole('link', { name: 'mgr Konrad Sołtys' })
        this.searchRoom = page.getByText('Nr pokoju: 4.19')
    }
}