export default {
  waveform: {
    data: {
      start_time: [
        {
          value: "reference_time",
          key: "Reference Time"
        },
        {
          value: "shock_time",
          key: "Shock Time"
        },
        {
          value: "p_arrival_time",
          key: "P Arrival Time"
        },
        {
          value: "s_arrival_time",
          key: "S Arrival Time"
        }
      ],
      model: [
        {
          value: "prem",
          key: "prem"
        },
        {
          value: "iasp91",
          key: "iasp91"
        },
        {
          value: "ak135",
          key: "ak135"
        }
      ],
      channal: [
        {
          value: "z",
          key: "vertical"
        },
        {
          value: "r",
          key: "radial"
        },
        {
          value: "t",
          key: "tangential"
        }
      ],
      axis: [
        {
          value: "epicenter_distance",
          key: "Epicenter Disnatce"
        },
        {
          value: "euclidean_distance",
          key: "Euclidean Distance"
        },
        {
          value: "depth",
          key: "Depth"
        }
      ]
    }
  },
  table: {
    columns_name: [
      {
        title: "ID",
        slot: "index",
        align: "center",
        fixed: "left"
      },
      {
        title: "Event",
        align: "center",
        children: [
          {
            title: "Start Time",
            key: "event_time",
            align: "center"
          },
          {
            title: "Latitude",
            key: "event_latitude",
            align: "center"
          },
          {
            title: "Longitude",
            key: "event_longitude",
            align: "center"
          },
          {
            title: "Depth",
            key: "event_depth",
            align: "center"
          },
          {
            title: "Magnitude",
            key: "event_magnitude",
            align: "center"
          }
        ]
      },
      {
        title: "Action",
        slot: "action",
        align: "center"
      }
    ]
  }
};
