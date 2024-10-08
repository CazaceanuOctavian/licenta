import React from "react";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";

export const Home: React.FC = () => {
    return (
        <h1>
            home page
            <div className="product-carousel-best-predicted-prices">
                <PopulateComponent userQuery="static" queryType="withBestPredictedPrices" productDisplayType="default"></PopulateComponent>
            </div>
        </h1>
    )
}