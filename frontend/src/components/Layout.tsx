import React, { useState, useEffect } from 'react';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  IconButton,
  Typography,
  Avatar,
  Menu,
  MenuItem,
  Divider,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  Person,
  Analytics,
  TableChart,
  Logout,
  ChevronLeft,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { authService } from '../services/authService';
import { apiService, UserProfile } from '../services/apiService';
import LoadingScreen from './LoadingScreen';

const drawerWidth = 280;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [desktopOpen, setDesktopOpen] = useState(true);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [isDataLoading, setIsDataLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
    setDesktopOpen(!desktopOpen);
  };

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfileClick = () => {
    navigate('/profile');
    handleProfileMenuClose();
  };

  const handleLogout = () => {
    authService.logout();
    handleProfileMenuClose();
  };

  useEffect(() => {
    const initializeApp = async () => {
      // Only try to load profile if user is authenticated
      if (!authService.isAuthenticated()) {
        return;
      }
      
      try {
        // Check if we need to load data by checking if profile exists
        const profile = await apiService.getUserProfile();
        setUserProfile(profile);
        
        // Check if data needs to be refreshed
        const dataStatus = await apiService.getDataStatus();
        if (!dataStatus.data_processed || !dataStatus.workflow_ready) {
          setIsDataLoading(true);
        }
      } catch (error) {
        console.error('Failed to load user profile:', error);
        // If it's an auth error, redirect to login
        if (error instanceof Error && error.message.includes('Authentication failed')) {
          authService.logout();
        }
      }
    };

    initializeApp();
  }, []);

  const handleDataLoadingComplete = () => {
    setIsDataLoading(false);
  };

  // Show loading screen if data is being loaded
  if (isDataLoading) {
    return <LoadingScreen onComplete={handleDataLoadingComplete} />;
  }

  const menuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/dashboard' },
    { text: 'Profile', icon: <Person />, path: '/profile' },
    { text: 'Analysis', icon: <Analytics />, path: '/analysis' },
    { text: 'Data', icon: <TableChart />, path: '/data' },
  ];

  const drawer = (
    <Box>
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: 2,
          borderBottom: '1px solid #333333',
        }}
      >
        <Typography variant="h5" fontWeight={700} color="primary">
          Strava Stats
        </Typography>
        <IconButton onClick={handleDrawerToggle} sx={{ color: 'text.secondary' }}>
          <ChevronLeft />
        </IconButton>
      </Box>
      <List sx={{ padding: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname === item.path}
              onClick={() => navigate(item.path)}
              sx={{
                borderRadius: 2,
                margin: '4px 8px',
                '&.Mui-selected': {
                  backgroundColor: '#ffffff',
                  color: '#000000',
                  '&:hover': {
                    backgroundColor: '#ffffff',
                  },
                  '& .MuiListItemIcon-root': {
                    color: '#000000',
                  },
                },
                '&:hover': {
                  backgroundColor: '#1a1a1a',
                },
              }}
            >
              <ListItemIcon sx={{ color: 'inherit' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      <AppBar
        position="fixed"
        sx={{
          width: { sm: desktopOpen ? `calc(100% - ${drawerWidth}px)` : '100%' },
          ml: { sm: desktopOpen ? `${drawerWidth}px` : 0 },
          backgroundColor: '#000000',
          borderBottom: '1px solid #333333',
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <IconButton
            color="inherit"
            aria-label="toggle drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { xs: 'none', sm: desktopOpen ? 'none' : 'block' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {menuItems.find(item => item.path === location.pathname)?.text || 'Dashboard'}
          </Typography>
          <IconButton
            size="large"
            edge="end"
            aria-label="account of current user"
            aria-controls="primary-search-account-menu"
            aria-haspopup="true"
            onClick={handleProfileMenuOpen}
            color="inherit"
          >
            <Avatar 
              src={userProfile?.profile} 
              sx={{ width: 32, height: 32, backgroundColor: '#ff6b35' }}
            >
              {userProfile?.firstname?.[0] || 'U'}
            </Avatar>
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box
        component="nav"
        sx={{ 
          width: { sm: desktopOpen ? drawerWidth : 0 }, 
          flexShrink: { sm: 0 },
          transition: 'width 0.3s ease'
        }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              backgroundColor: '#000000',
              borderRight: '1px solid #333333',
            },
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
              backgroundColor: '#000000',
              borderRight: '1px solid #333333',
              transition: 'transform 0.3s ease',
              transform: desktopOpen ? 'translateX(0)' : 'translateX(-100%)',
            },
          }}
          open={desktopOpen}
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: desktopOpen ? `calc(100% - ${drawerWidth}px)` : '100%' },
          backgroundColor: '#000000',
          minHeight: '100vh',
          transition: 'width 0.3s ease',
          overflow: 'auto',
        }}
      >
        <Toolbar />
        {children}
      </Box>
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleProfileMenuClose}
        PaperProps={{
          sx: {
            backgroundColor: '#111111',
            border: '1px solid #333333',
            mt: 1,
          },
        }}
      >
        <MenuItem onClick={handleProfileClick}>
          <ListItemIcon>
            <Person fontSize="small" />
          </ListItemIcon>
          <ListItemText>Profile</ListItemText>
        </MenuItem>
        <Divider sx={{ backgroundColor: '#333333' }} />
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          <ListItemText>Logout</ListItemText>
        </MenuItem>
      </Menu>
    </Box>
  );
};

export default Layout;