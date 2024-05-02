export interface Order {
  customer: Customer;
  customer_selection: CustomerSelection[];
  city: number;
  station: number;
  month: number;
  block_position: number;
  other_person_rate?: boolean;
  hour_selected_rate?: boolean;
}

export type OrderPdf = Omit<Order, 'customer'>;

export type Customer = {
  company_name?: string;
  name: string;
  phone: string;
  email?: string;
};

export type CustomerSelection = {
  date: number;
  time_interval: number;
  audio_duration: number;
};
