import React from "react";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";

export const Home: React.FC = () => {
    return (
        <div id="root">
            <h1 className="main-title">
                home page
            </h1>
            <div className="products-best-predicted-prices">
                <h4 className="informative">Prezicem ca urmatoarele produse vor avea cele mai mari ieftiniri in viitor:</h4>
                <PopulateComponent userQuery="static" queryType="withBestPredictedPrices" productDisplayType="default"></PopulateComponent>
            </div>
            <div className="products-lowest-current-prices">
                <h4 className="informative">Urmatoarele produse au cel mai ieftin pret de pana acum:</h4>
                <PopulateComponent userQuery="static" queryType="withLowestHistoricalPrices" productDisplayType="default"></PopulateComponent>
            </div>
        </div>
    )
}