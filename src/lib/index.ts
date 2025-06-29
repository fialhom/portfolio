export type PortfolioItem = {
    id: string;
    category: string;
    title: string;
    date: string;
    description: string;
    local: Boolean;
    url: string;
    tags: Array<string>;
    username: string;
    image: Boolean;
    image_url?: string;
}

export type MetaFields = {
    lastupdate: string;
    totalitems: number;
}
export type PortfolioData = {
    items: Array<PortfolioItem>;
    meta_info: MetaFields;
}
