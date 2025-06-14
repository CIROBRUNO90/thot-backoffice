document.addEventListener('DOMContentLoaded', function() {
    // Función para calcular el total
    function calculateTotal() {
        const subtotalField = document.getElementById('id_product_subtotal');
        const discountField = document.getElementById('id_discount');
        const shippingField = document.getElementById('id_shipping_cost');
        const totalField = document.getElementById('id_total');
        
        if (subtotalField && discountField && shippingField && totalField) {
            const subtotal = parseFloat(subtotalField.value) || 0;
            const discount = parseFloat(discountField.value) || 0;
            const shipping = parseFloat(shippingField.value) || 0;
            
            const total = subtotal - discount + shipping;
            
            // Actualizar el campo total
            totalField.value = total.toFixed(2);
            
            // Cambiar color si el total es 0 o negativo
            if (total <= 0) {
                totalField.style.backgroundColor = '#ffebee';
                totalField.style.color = '#c62828';
            } else {
                totalField.style.backgroundColor = '#e8f5e8';
                totalField.style.color = '#2e7d32';
            }
        }
    }
    
    // Agregar event listeners a los campos que afectan el total
    const fieldsToWatch = ['id_product_subtotal', 'id_discount', 'id_shipping_cost'];
    
    fieldsToWatch.forEach(function(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', calculateTotal);
            field.addEventListener('change', calculateTotal);
            field.addEventListener('blur', calculateTotal);
        }
    });
    
    // Calcular total inicial
    calculateTotal();
    
    // Prevenir envío si el total es 0 o negativo
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const totalField = document.getElementById('id_total');
            if (totalField) {
                const total = parseFloat(totalField.value) || 0;
                if (total <= 0) {
                    e.preventDefault();
                    alert('Error: El total debe ser mayor que 0. Verifique el subtotal, descuento y costo de envío.');
                    return false;
                }
            }
        });
    }
});