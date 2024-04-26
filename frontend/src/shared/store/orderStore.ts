import { AdOrderSettings, Customer, CustomerSelection, OrderState } from 'shared/types';
import { create } from 'zustand';

export const useOrder = create<OrderState>()((set) => ({
  customer: null,
  adOrderSettings: null,
  customer_selection: [],
  setCustomer: (customer: Customer) => set({ customer }),
  setAdOrderSettings: (adOrderSettings: AdOrderSettings) => set({ adOrderSettings }),
  setCustomerSelection: (customer_selection: CustomerSelection) =>
    set((state) => ({ customer_selection: [...state.customer_selection, customer_selection] })),
  deleteCustomerSelection: (customer_selection: CustomerSelection) =>
    set((state) => ({
      customer_selection: state.customer_selection?.filter(
        (selection) =>
          selection.date !== customer_selection.date || selection.time_interval !== customer_selection.time_interval
      )
    })),
  clearCustomerSelections: () => set({ customer_selection: [] })
}));
