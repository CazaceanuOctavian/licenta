// interpretPath.ts
const interpretPath = (): string => {
    let currentHref: string = window.location.href;
    var hrefArray = currentHref.split('/');

    if (hrefArray.includes('search')) {
        console.log('returning the search query: http://localhost:8080/products/name/search=');
        return 'http://localhost:8080/products/name/search=';
    }
    else if (hrefArray.includes('current_product')) {
        console.log('returning the details query: http://localhost:8080/products/code/search=');
        return 'http://localhost:8080/products/code/search=';
    }

    return 'err';
};

export default interpretPath;
