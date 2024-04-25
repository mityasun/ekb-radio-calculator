import { CityModel } from './cityModels';

export interface RadioModel {
  id: number;
  default: boolean;
  name: string;
}

export interface AudienceSex {
  id: number;
  sex: 'Женщины' | 'Мужчины';
  percent: number;
}

export interface AudienceAge {
  id: number;
  age: string;
  percent: number;
}

export interface MonthRate {
  id: number;
  month:
    | 'Январь'
    | 'Февраль'
    | 'Март'
    | 'Апрель'
    | 'Май'
    | 'Июнь'
    | 'Июль'
    | 'Август'
    | 'Сентябрь'
    | 'Октябрь'
    | 'Ноябрь'
    | 'Декабрь';
  rate: number;
}

export interface BlockPositionRate {
  id: number;
  block_position: string;
  rate: number;
}

export interface IntervalPrice {
  id: number;
  time_interval: string;
  audio_duration: number;
  interval_price: number;
}

export interface AmountDiscount {
  id: number;
  order_amount: number;
  discount: number;
}

export interface DayDiscount {
  id: number;
  total_days: number;
  discount: number;
}

export interface VolumeDiscount {
  id: number;
  order_volume: number;
  discount: number;
}

export interface RadioFullModel extends RadioModel {
  title: string;
  description: string;
  city: CityModel;
  broadcast_zone: string;
  reach_dly: number | null;
  reach_dly_percent: number | null;
  other_person_rate: number;
  hour_selected_rate: number;
  logo: string;
  audience_sex: AudienceSex[] | [];
  audience_age: AudienceAge[] | [];
  month_rate: MonthRate[];
  block_position_rate: BlockPositionRate[];
  intrval_price: IntervalPrice[];
  amount_discount: AmountDiscount[];
  days_discount: DayDiscount[];
  volume_discount: VolumeDiscount[];
}

export interface RadioState {
  radios: RadioModel[];
  selectedRadioId: number | null;
  selectedRadio: RadioFullModel | null;
  setRadios: (radios: RadioModel[]) => void;
  setSelectedRadio: (radio: RadioFullModel | null) => void;
  setSelectedRadioId: (radioId: number | null) => void;
}
