import { useEffect, useState } from "react";
import Search from "./SearchComponent"

interface SearchProps {
    userQuery: string;
    displayType: string
    setUserQuery: (query: string) => void;
    selectedValue: string;
    setSelectedValue: (query: string) => void;
    selectedPage: number
    setSelectedPage: (query: number) => void;
    maxPages:string
}

interface SwitchComponentProps {
    displayType: string
}

const Navbar: React.FC<SearchProps> = ( {displayType, setUserQuery, userQuery, selectedValue, setSelectedValue, selectedPage, setSelectedPage, maxPages} ) => {
    
    const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedValue(event.target.value);
      };

    const increment = () => {
        if(selectedPage + 1 <= Number.parseInt(maxPages)) {
            window.scrollTo({ top: 0, behavior: 'instant' }); 
            setSelectedPage(selectedPage + 1)
        }
    }

    const decrement = () => {
        if (selectedPage > 1 && selectedPage - 1 > 0) {
            window.scrollTo({ top: 0, behavior: 'instant' }); 
            setSelectedPage(selectedPage - 1)
        }
    }

    useEffect(() => {
        //set maxPages > 0 condition to fix bug where when a search would yield nothing
        //the page was set to 0 which made the database return error 500 and would stop
        //searches until next button was pressed or page refresh
        if(Number.parseInt(maxPages) == 0) {
            maxPages='1'
        }

        if(selectedPage > Number.parseInt(maxPages)) {
             setSelectedPage(Number.parseInt(maxPages))
        }
    }, [maxPages, selectedPage]);

    const ContextComponent: React.FC<SwitchComponentProps> = ({ displayType }) => {
        switch (displayType) {
            case "withFullFeatures":
                return (
                    <div className="nav-baar">
                        <div className="search-container">
                            <button className="prev-button" onClick={decrement}>prev</button>
                            <Search userQuery={userQuery} setUserQuery={setUserQuery} />
                            <button className="next-button" onClick={increment}>next</button>
                        </div>
                        <select id="count-dropdown" value={selectedValue} onChange={handleSelectChange}>
                            <option value="">--Select--</option>
                            <option value="20">20 Elemente</option>
                            <option value="40">40 Elemente</option>
                            <option value="60">60 Elemente</option>
                        </select>
                    </div>
                );
            case "withOnlyButtons":
                return (
                    <div className="nav-baar">
                        <div className="search-container">
                            <button className="prev-button-bottom" onClick={decrement}>prev</button>
                            <button className="next-button-bottom" onClick={increment}>next</button>
                        </div>
                    </div>
                );
            default:
                return null;
        }
    }
  
    return <ContextComponent displayType={displayType}></ContextComponent>
}

export default Navbar