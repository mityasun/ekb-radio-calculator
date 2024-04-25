const mockData = [
  {
    id: 1,
    default: false,
    name: 'Москва'
  },
  {
    id: 2,
    default: false,
    name: 'Санкт-Петербург'
  },
  {
    id: 3,
    default: false,
    name: 'Казань'
  },
  {
    id: 4,
    default: false,
    name: 'Ростов-на-Дону'
  },
  {
    id: 5,
    default: true,
    name: 'Екатеринбург'
  },
  {
    id: 6,
    default: false,
    name: 'Волгоград'
  },
  {
    id: 7,
    default: false,
    name: 'Омск'
  },
  {
    id: 8,
    default: false,
    name: 'Новосибирск'
  }
];

export const getCities = async () => {
  const response = { data: mockData };
  return response.data;
};
