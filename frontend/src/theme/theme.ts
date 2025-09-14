import { createTheme } from '@mui/material/styles';

export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff6b35', // Orange highlight color
      light: '#ff8a65',
      dark: '#e64a19',
    },
    secondary: {
      main: '#ffffff',
      light: '#ffffff',
      dark: '#cccccc',
    },
    background: {
      default: '#000000',
      paper: '#111111',
    },
    text: {
      primary: '#ffffff',
      secondary: '#aaaaaa',
    },
    divider: '#333333',
  },
  typography: {
    fontFamily: [
      'Inter',
      'Roboto',
      'Poppins',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Arial',
      'sans-serif',
    ].join(','),
    fontWeightMedium: 600,
    fontWeightBold: 700,
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 600,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 600,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 12,
  },
  spacing: 8,
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: 'none',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#111111',
          border: '1px solid #333333',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#000000',
          borderRight: '1px solid #333333',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#000000',
          boxShadow: 'none',
          borderBottom: '1px solid #333333',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          margin: '4px 8px',
          '&.Mui-selected': {
            backgroundColor: '#ffffff',
            color: '#000000',
            '&:hover': {
              backgroundColor: '#ffffff',
            },
          },
          '&:hover': {
            backgroundColor: '#1a1a1a',
          },
        },
      },
    },
  },
});