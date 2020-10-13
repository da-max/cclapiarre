// Types

export interface SubItem {
  readonly name: string,
  readonly link: string
}

export interface NavbarItem {
  readonly title: string,
  readonly subItems?: SubItem[],
  readonly link?: string
}
