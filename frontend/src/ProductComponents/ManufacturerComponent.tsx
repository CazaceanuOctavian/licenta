import React, { useEffect, useState } from 'react';

interface selectedManufacturers{
    selectedManufacturers: string[]
    setSelectedManufacturers: (query: string[]) =>void

    data:string[]
;}

export const ManufacturerListComponent: React.FC<selectedManufacturers> = ({ data, selectedManufacturers, setSelectedManufacturers }) => {
    const [checkedItems, setCheckedItems] = useState<string[]>([]);

    const handleCheckboxChange = (item: string) => {
        setCheckedItems(prevState => {
            if (prevState.includes(item)) {
                // Item is already checked, remove it from the list
                return prevState.filter(checkedItem => checkedItem !== item);
                
            } else {
                // Item is not checked, add it to the list
                return [...prevState, item];
            }
        });
    };

    const getCheckedItems = () => {
        console.log(checkedItems); // You can return or use this list as needed
        return checkedItems;
    };

    useEffect(() => {
        setSelectedManufacturers(checkedItems)
    }, [checkedItems])
    
    return (
        <div className="manufacturer-container">
            <ul className="manufacturer-list">
                {data.map(item => (
                    <li key={item}>
                        <label>
                            <input
                                type="checkbox"
                                checked={checkedItems.includes(item)}
                                onChange={() => handleCheckboxChange(item)}
                            /> {item}
                        </label>
                    </li>
                ))}
            </ul>
            <button onClick={getCheckedItems}>Get Checked Items</button>
        </div>
    );
};
