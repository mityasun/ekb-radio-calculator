import axios from 'axios';
import saveAs from 'file-saver';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { OrderPdf } from 'shared/types';

export const postOrderPdf = async (orderPdf: OrderPdf) =>
  axios({
    url: `${apiBaseUrl}/api/order-pdf/`,
    data: orderPdf,
    method: 'POST',
    withCredentials: false,
    responseType: 'blob',
    headers: {
      'Content-Type': 'application/json'
    }
  }).then((response) => {
    const file = new Blob([response.data], { type: 'application/pdf' });
    const timeString = new Date()
      .toLocaleString('ru', { dateStyle: 'short', timeStyle: 'medium' })
      .replace(/:/g, '.')
      .replace(/, /g, '_');
    saveAs(file, `Taksa_Radio_${timeString}.pdf`);
  });
