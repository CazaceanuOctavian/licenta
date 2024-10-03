interface Manufacturer{
    data:string[]
}

export const ManufacturerListComponent: React.FC<Manufacturer> = ({ data }) => {
    return (
        <div className="manufacturer-container">
            <ul className="manufacturer-list">
            {data.map(item => (
             <li>
                <label>
                    <input type="checkbox" id="item4" /> {item}
                </label>
           </li>
            ))}
            </ul>
        </div>
    );
};
