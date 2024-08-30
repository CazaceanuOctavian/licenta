import PopulateComponent from "./PopulatePageComponent";
import interpretPath from "./InterpretPathFunc";

const ProductDetailsComponent: React.FC = () => {
    var product_id = window.location.href.split('=')[1]

    return (
        <div className='page'>
            <div className='fist-section'>this is the product details section</div>
            <PopulateComponent productDisplayType="detailed" userQuery={product_id}></PopulateComponent>
        </div>
        
    );
  }

export default ProductDetailsComponent