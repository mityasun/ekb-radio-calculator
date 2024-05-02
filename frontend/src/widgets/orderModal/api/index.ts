import axios, { AxiosResponse } from 'axios';
import { apiBaseUrl } from 'shared/constants/apiBaseUrl';
import { Order } from 'shared/types';

type Error400 = {
  status: 400;
  error: string;
};

type Error404 = {
  status: 404;
  detail: string;
};

export type ApiOrderError = Error400 | Error404;

export const postOrder = async (order: Order): Promise<AxiosResponse<void, ApiOrderError>> =>
  axios({
    url: `${apiBaseUrl}/api/order/`,
    data: order,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  });
