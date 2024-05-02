import { UseMutationResult } from '@tanstack/react-query';
import { AxiosResponse } from 'axios';
import { appSettings, CityModel, Customer, CustomerSelection, Order, RadioFullModel } from 'shared/types';
import { ApiOrderError } from '../api';

export const submitOrder = (
  customerDirty: Customer,
  customer_selection: CustomerSelection[],
  selectedCity: CityModel | null,
  selectedRadio: RadioFullModel | null,
  appSettings: appSettings,
  mutation: UseMutationResult<AxiosResponse<void, ApiOrderError>, Error, Order, unknown>
) => {
  const customer = Object.fromEntries(Object.entries(customerDirty).filter(([_, value]) => value !== '')) as Customer;

  if (!selectedRadio || !appSettings.month || !appSettings.block_position || !selectedCity) return;

  const response: Order = {
    customer,
    station: selectedRadio.id,
    month: appSettings.month.id,
    block_position: appSettings.block_position.id,
    other_person_rate: appSettings.other_person_rate,
    hour_selected_rate: appSettings.hour_selected_rate,
    city: selectedCity.id,
    customer_selection
  };

  if (!response) return;

  mutation.mutate(response);
};
