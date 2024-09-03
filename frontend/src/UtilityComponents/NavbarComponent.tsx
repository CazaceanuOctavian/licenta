import { useState } from "react";
import Search from "./SearchComponent"

const Navbar: React.FC = () => {
    const [userQuery, setUserQuery] = useState<string>('');
    const [selectedValue, setSelectedValue] = useState<string>("");

    const handleSelectChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setSelectedValue(event.target.value);
      };

    return (
        <div>
            <Search userQuery="" setUserQuery={setUserQuery}></Search>
            <select id="dropdown" value={selectedValue} onChange={handleSelectChange}>
                <option value="">--Select--</option>
                <option value="20">20 Elemente</option>
                <option value="40">40 Elemente</option>
                <option value="60">60 Elemente</option>
            </select>
        </div>
    )
}

export default Navbar