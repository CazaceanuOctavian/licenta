import { useState } from "react";
import Search from "./SearchComponent"

interface SearchProps {
    userQuery: string;
    setUserQuery: (query: string) => void;
    selectedValue: string;
    setSelectedValue: (query: string) => void;
    selectedPage: number
    setSelectedPage: (query: number) => void;
}

const Navbar: React.FC<SearchProps> = ( {userQuery, setUserQuery, selectedValue, setSelectedValue, selectedPage, setSelectedPage} ) => {

    const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedValue(event.target.value);
      };

    const increment = () => {
        setSelectedPage(selectedPage + 1)
    }

    const decrement = () => {
        setSelectedPage(selectedPage - 1)
    }

    return (
        <div>
            <Search userQuery="" setUserQuery={setUserQuery}></Search>
            <select id="count_dropdown" value={selectedValue} onChange={handleSelectChange}>
                <option value="">--Select--</option>
                <option value="20">20 Elemente</option>
                <option value="40">40 Elemente</option>
                <option value="60">60 Elemente</option>
            </select>
            <button onClick={decrement}>
                prev
            </button>
            <button onClick={increment}>
                next
            </button>
        </div>
    )
}

export default Navbar