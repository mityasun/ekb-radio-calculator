export interface Order extends AdOrderSettings {
  customer: Customer;
  customer_selection: CustomerSelection[];
}

export type Customer = {
  company_name: string;
  name: string;
  phone: string;
  email: string;
};

export type CustomerSelection = {
  date: number;
  time_interval: number;
  audio_duration: number;
};

export type TimeInterval = {
  id: number;
  time_interval: string;
};

export type AdOrderSettings = {
  city: number;
  station: number;
  month: number;
  block_position: number;
  other_person_rate: boolean;
  hour_selected_rate: boolean;
};

export interface OrderState {
  customer: Customer | null;
  adOrderSettings: AdOrderSettings | null;
  customer_selection: CustomerSelection[] | [];
  setCustomer: (customer: Customer) => void;
  setAdOrderSettings: (adOrderSettings: AdOrderSettings) => void;
  setCustomerSelection: (customer_selection: CustomerSelection) => void;
  deleteCustomerSelection: (customer_selection: CustomerSelection) => void;
  clearCustomerSelections: () => void;
}
