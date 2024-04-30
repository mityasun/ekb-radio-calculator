import axios from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { Order } from 'shared/types';

export const postOrder = (order: Order) =>
  axios({
    url: `${apiBaseUrl}/api/order/`,
    data: order,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json'
    }
  });
