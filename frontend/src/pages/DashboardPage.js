import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Box, 
  Typography, 
  Paper, 
  Button, 
  AppBar, 
  Toolbar, 
  IconButton, 
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  Card,
  CardContent,
  Grid,
  CircularProgress,
  Alert
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Dashboard as DashboardIcon,
  Person as PersonIcon,
  Work as WorkIcon,
  ExitToApp as LogoutIcon
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const DashboardPage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [applicantsCount, setApplicantsCount] = useState(null);
  const [vacanciesCount, setVacanciesCount] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        const applicantsResponse = await axios.get('/api/candidates/?page=1&page_size=1');
        setApplicantsCount(applicantsResponse.data.total);
        
        const vacanciesResponse = await axios.get('/api/job-vacancies/?page=1&page_size=1');
        setVacanciesCount(vacanciesResponse.data.total);
        
        setError('');
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load dashboard data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const navigateTo = (path) => {
    navigate(path);
  };

  const drawerContent = (
    <Box sx={{ width: 250 }} role="presentation">
      <Box sx={{ p: 2 }}>
        <Typography variant="h6" color="primary">Sombra Recruitment</Typography>
        <Typography variant="body2" color="text.secondary">
          {user?.email}
        </Typography>
      </Box>
      <Divider />
      <List>
        <ListItem button selected>
          <ListItemIcon>
            <DashboardIcon color="primary" />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItem>
        <ListItem button onClick={() => navigateTo('/applicants')}>
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <ListItemText primary="Applicants" />
        </ListItem>
        <ListItem button onClick={() => navigateTo('/job-vacancies')}>
          <ListItemIcon>
            <WorkIcon />
          </ListItemIcon>
          <ListItemText primary="Job Vacancies" />
        </ListItem>
      </List>
      <Divider />
      <List>
        <ListItem button onClick={logout}>
          <ListItemIcon>
            <LogoutIcon />
          </ListItemIcon>
          <ListItemText primary="Logout" />
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={toggleDrawer}
            sx={{ mr: 2 }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Sombra Recruitment Dashboard
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>
      
      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer}
      >
        {drawerContent}
      </Drawer>
      
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          backgroundColor: (theme) => theme.palette.background.default,
          minHeight: '100vh'
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="h4" gutterBottom>
            Welcome to Sombra Recruitment System
          </Typography>
          
          <Typography variant="body1" paragraph>
            This system helps recruiters select better job candidates by matching applicant profiles with job vacancies.
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}
          
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h5" color="primary" gutterBottom>
                    Applicants
                  </Typography>
                  {loading ? (
                    <Box display="flex" justifyContent="center" my={3}>
                      <CircularProgress />
                    </Box>
                  ) : (
                    <>
                      <Typography variant="h3" component="div">
                        {applicantsCount !== null ? applicantsCount : 'N/A'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Total applicants in the system
                      </Typography>
                    </>
                  )}
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h5" color="primary" gutterBottom>
                    Job Vacancies
                  </Typography>
                  {loading ? (
                    <Box display="flex" justifyContent="center" my={3}>
                      <CircularProgress />
                    </Box>
                  ) : (
                    <>
                      <Typography variant="h3" component="div">
                        {vacanciesCount !== null ? vacanciesCount : 'N/A'}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Total job vacancies available
                      </Typography>
                      <Box mt={2}>
                        <Button 
                          variant="contained" 
                          color="primary"
                          onClick={() => navigateTo('/job-vacancies')}
                        >
                          View Job Vacancies
                        </Button>
                      </Box>
                    </>
                  )}
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12}>
              <Paper sx={{ p: 3, mt: 3 }}>
                <Typography variant="h5" gutterBottom>
                  Getting Started
                </Typography>
                <Typography variant="body1" paragraph>
                  Use the navigation menu to access applicants and job vacancies. You can:
                </Typography>
                <ul>
                  <li>View and search applicant profiles</li>
                  <li>Browse available job vacancies</li>
                  <li>Match candidates with suitable positions</li>
                  <li>Generate reports on recruitment progress</li>
                </ul>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
};

export default DashboardPage;
