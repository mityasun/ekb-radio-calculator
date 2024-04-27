import axios from 'axios';
import saveAs from 'file-saver';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { OrderPdf } from 'shared/types';

export const getOrderPdf = (orderPdf: OrderPdf) =>
  axios({
    url: `${apiBaseUrl}/api/order-pdf/`,
    data: orderPdf,
    method: 'POST',
    responseType: 'blob'
  }).then((response) => {
    const file = new Blob([response.data], { type: 'application/pdf' });
    saveAs(file, 'TaksaOrderPreviw.pdf');
  });
