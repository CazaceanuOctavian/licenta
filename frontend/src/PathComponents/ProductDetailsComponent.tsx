import GraphComponent from "../UtilityComponents/GraphComponent";
import PopulateComponent from "../UtilityComponents/PopulatePageComponent";

const ProductDetailsComponent: React.FC = () => {
    var product_id = window.location.href.split('=')[1]

    return (
        <div className='page'>
            <div className='fist-section'>this is the product details section</div>
            <div className='product-detailes'>
                <PopulateComponent productDisplayType="detailed" queryType="withProductCode" userQuery={product_id}></PopulateComponent>
            </div>
            <div className='statistics'>
                <h1>
                    Statistics
                    <p>
                        statistics will go here at some point
                    </p>
                    <GraphComponent />
                </h1>
            </div>
        </div>
    );
  }

export default ProductDetailsComponent