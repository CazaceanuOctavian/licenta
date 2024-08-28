async function getData(url: string): Promise<void> {
    try {
        console.log('trying to fetch...')
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`HTTP error with Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data);
        console.log('fetch succesful')
        return data
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}


export default getData;
