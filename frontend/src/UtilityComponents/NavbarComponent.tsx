import { useState } from "react";
import Search from "./SearchComponent"

interface SearchProps {
    userQuery: string;
    displayType: string
    setUserQuery: (query: string) => void;
    selectedValue: string;
    setSelectedValue: (query: string) => void;
    selectedPage: number
    setSelectedPage: (query: number) => void;
}

interface SwitchComponentProps {
    displayType: string
}

const Navbar: React.FC<SearchProps> = ( {displayType, setUserQuery, selectedValue, setSelectedValue, selectedPage, setSelectedPage} ) => {

    const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedValue(event.target.value);
      };

    const increment = () => {
        window.scrollTo({ top: 0, behavior: 'instant' }); 
        setSelectedPage(selectedPage + 1)
    }

    const decrement = () => {
        if (selectedPage > 1)
            window.scrollTo({ top: 0, behavior: 'instant' }); 
            setSelectedPage(selectedPage - 1)
    }


    const ContextComponent: React.FC<SwitchComponentProps> = ({ displayType }) => {
        switch (displayType) {
            case "withFullFeatures":
                return (
                    <div className="nav-baar">
                        <div className="search-container">
                            <button className="prev-button" onClick={decrement}>prev</button>
                            <Search userQuery="" setUserQuery={setUserQuery} />
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